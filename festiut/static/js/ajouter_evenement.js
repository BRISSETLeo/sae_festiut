function previewImage() {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  const imagePreviewContainer = document.getElementById('previewImageContainer');
  
  if(file.type.match('image.*')){
    const reader = new FileReader();
    
    reader.addEventListener('load', function (event) {
      const imageUrl = event.target.result;
      const image = new Image();
      
      image.addEventListener('load', function() {
        imagePreviewContainer.removeChild(imagePreviewContainer.lastChild);
        imagePreviewContainer.appendChild(image);
      });
      
      image.src = imageUrl;
      image.style.width = 'auto';
      image.style.height = 'auto';
    });
    
    reader.readAsDataURL(file);
  }
}