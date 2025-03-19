
document.getElementById('fileInput').addEventListener('change', function(event)
{
        var file = event.target.files[event.target.files.length - 1];
        var fileInfo = `
                <p>File Name: ${file.name}</p>
                <p>File Size: ${file.size} bytes</p>
                <p>File Type: ${file.type}</p>
        `;

        var image = document.createElement('img');
        image.src = URL.createObjectURL(file);
        image.style.height = '100px';
        image.style.display = 'block';
        image.style.marginBottom = '10px';

        preview.getElementById('preview').innerHTML = image;

        document.getElementById('fileInfo').innerHTML = fileInfo;
});

function start()
{
        fetch("https://cis655-vision-api-project.ue.r.appspot.com/get-image-description")
        .then(response => response.json())
        .then(data =>
        {
                console.log(data)

                document.getElementById("Problem").innerText = "Most likely: " + data['labels'][0]['description'] + " with a score of: " + data['labels'][0]['score'];
        })
        .catch(error => console.error("Error fetching description:", error));
}