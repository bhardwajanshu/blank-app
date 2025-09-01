"""
Batch processing functionality for handling multiple product images
"""
import asyncio
import concurrent.futures
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

from shopify_client import ShopifyClient
from photoroom_client import PhotoRoomClient
from config import MAX_BATCH_SIZE


@dataclass
class ProcessingResult:
    """Result of processing a single image"""
    product_id: int
    image_id: int
    original_url: str
    success: bool
    processed_data: Optional[bytes] = None
    error_message: Optional[str] = None
    processing_time: Optional[float] = None


class BatchProcessor:
    def __init__(self):
        self.shopify_client = ShopifyClient()
        self.photoroom_client = PhotoRoomClient()
        self.processing_history = []
    
    def get_product_images_for_selection(self) -> List[Dict]:
        """Get all product images formatted for UI selection"""
        try:
            all_images = self.shopify_client.get_all_product_images()
            return all_images
        except Exception as e:
            raise Exception(f"Failed to fetch product images: {str(e)}")
    
    def process_single_image(self, image_info: Dict, operation: str, **kwargs) -> ProcessingResult:
        """Process a single image with PhotoRoom API"""
        start_time = datetime.now()
        
        try:
            # Process the image
            processed_data = self.photoroom_client.process_image_from_url(
                image_info['image_url'], 
                operation, 
                **kwargs
            )
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            return ProcessingResult(
                product_id=image_info['product_id'],
                image_id=image_info['image_id'],
                original_url=image_info['image_url'],
                success=True,
                processed_data=processed_data,
                processing_time=processing_time
            )
        
        except Exception as e:
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            return ProcessingResult(
                product_id=image_info['product_id'],
                image_id=image_info['image_id'],
                original_url=image_info['image_url'],
                success=False,
                error_message=str(e),
                processing_time=processing_time
            )
    
    def process_batch(self, selected_images: List[Dict], operation: str, **kwargs) -> Dict[str, Any]:
        """Process multiple images in parallel batches"""
        if not selected_images:
            return {'results': [], 'summary': {'total': 0, 'successful': 0, 'failed': 0}}
        
        # Split into batches if necessary
        batches = [selected_images[i:i + MAX_BATCH_SIZE] 
                  for i in range(0, len(selected_images), MAX_BATCH_SIZE)]
        
        all_results = []
        
        for batch_idx, batch in enumerate(batches):
            print(f"Processing batch {batch_idx + 1}/{len(batches)} ({len(batch)} images)")
            
            # Process batch in parallel using ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                future_to_image = {
                    executor.submit(self.process_single_image, image_info, operation, **kwargs): image_info
                    for image_info in batch
                }
                
                batch_results = []
                for future in concurrent.futures.as_completed(future_to_image):
                    result = future.result()
                    batch_results.append(result)
                
                all_results.extend(batch_results)
        
        # Generate summary
        successful_results = [r for r in all_results if r.success]
        failed_results = [r for r in all_results if not r.success]
        
        summary = {
            'total': len(all_results),
            'successful': len(successful_results),
            'failed': len(failed_results),
            'success_rate': len(successful_results) / len(all_results) * 100 if all_results else 0,
            'total_processing_time': sum(r.processing_time or 0 for r in all_results),
            'operation': operation,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store in processing history
        self.processing_history.append({
            'summary': summary,
            'results': all_results
        })
        
        return {
            'results': all_results,
            'summary': summary
        }
    
    def upload_processed_images_to_shopify(self, processing_results: List[ProcessingResult], replace_original: bool = True) -> Dict[str, Any]:
        """Upload processed images back to Shopify"""
        upload_results = {
            'successful_uploads': [],
            'failed_uploads': [],
            'summary': {}
        }
        
        successful_results = [r for r in processing_results if r.success and r.processed_data]
        
        for result in successful_results:
            try:
                filename = f"processed_{result.image_id}.png"
                
                if replace_original:
                    # Update existing image
                    uploaded_image = self.shopify_client.update_product_image(
                        result.product_id,
                        result.image_id,
                        result.processed_data,
                        filename
                    )
                else:
                    # Create new image
                    uploaded_image = self.shopify_client.upload_image_to_product(
                        result.product_id,
                        result.processed_data,
                        filename,
                        alt_text="AI processed image"
                    )
                
                upload_results['successful_uploads'].append({
                    'product_id': result.product_id,
                    'image_id': result.image_id,
                    'new_image_info': uploaded_image
                })
                
            except Exception as e:
                upload_results['failed_uploads'].append({
                    'product_id': result.product_id,
                    'image_id': result.image_id,
                    'error': str(e)
                })
        
        upload_results['summary'] = {
            'total_processed': len(successful_results),
            'successful_uploads': len(upload_results['successful_uploads']),
            'failed_uploads': len(upload_results['failed_uploads']),
            'upload_success_rate': len(upload_results['successful_uploads']) / len(successful_results) * 100 if successful_results else 0
        }
        
        return upload_results
    
    def get_processing_history(self) -> List[Dict]:
        """Get the history of all processing operations"""
        return self.processing_history
    
    def export_results(self, results: Dict, filename: str = None) -> str:
        """Export processing results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"processing_results_{timestamp}.json"
        
        # Convert ProcessingResult objects to dictionaries for JSON serialization
        exportable_results = results.copy()
        if 'results' in exportable_results:
            exportable_results['results'] = [
                {
                    'product_id': r.product_id,
                    'image_id': r.image_id,
                    'original_url': r.original_url,
                    'success': r.success,
                    'error_message': r.error_message,
                    'processing_time': r.processing_time,
                    'has_processed_data': r.processed_data is not None
                }
                for r in exportable_results['results']
            ]
        
        with open(filename, 'w') as f:
            json.dump(exportable_results, f, indent=2)
        
        return filename