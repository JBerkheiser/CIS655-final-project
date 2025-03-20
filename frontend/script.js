
document.getElementById('fileInput').addEventListener('change', function(event)
{
        var file = event.target.files[event.target.files.length - 1];
        var image = URL.createObjectURL(file);
        var fileInfo = `
                <p>File Name: ${file.name}</p>
                <p>File Size: ${file.size} bytes</p>
                <p>File Type: ${file.type}</p>
                <p>File URL: ${image}</p>
        `;
        var imagePreview = `
                <img src="${image}" alt="Could Not Load Image" width="500" height="600">
        `;

        document.getElementById('preview').innerHTML = imagePreview;

        document.getElementById('fileInfo').innerHTML = fileInfo;
});

async function start()
{
        const imageInput = document.getElementById('fileInput');
        if(!imageInput.files.length)
        {
                alert("Please select a file");
                return;
        } 

        const formData = new FormData();
        formData.append("file", imageInput.files[imageInput.files.length - 1]);

        try
        {
                const response = await fetch("https://cis655-vision-api-project.ue.r.appspot.com/get-image-description", 
                {
                        method: "POST",
                        body: formData,
                })
                const result = await response.json();
                console.log("Server Response:", result);
                document.getElementById("Problem").innerText = "Most likely: " + result['labels'][0]['description'] + " with a score of: " + result['labels'][0]['score'];
        } catch(error)
        {
                console.error("Error fetching description:", error);
        }
}