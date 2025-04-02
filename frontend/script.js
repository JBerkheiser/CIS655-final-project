var queryTable = [
        {id: "LABEL_DETECTION", checked: 0},
        {id: "FACE_DETECTION", checked: 0},
        {id: "LANDMARK_DETECTION", checked: 0},
        {id: "LOGO_DETECTION", checked: 0},
        {id: "DOCUMENT_TEXT_DETECTION", checked: 0},
        {id: "OBJECT_LOCALIZATION", checked: 0},
];

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
                <img src="${image}" alt="Could Not Load Image">
        `;

        document.getElementById('preview').innerHTML = imagePreview;
});

async function analyzeImage()
{       
        const imageInput = document.getElementById('fileInput');
        if(!imageInput.files.length)
        {
                alert("Please select a file");
                return;
        } 

        getCheckedBoxes();

        const formData = new FormData();
        formData.append("file", imageInput.files[imageInput.files.length - 1]);

        var detectionTasks = []
        for(var i = 0; i < queryTable.length; i++)
        {
                if(queryTable[i].checked === true)
                {
                        detectionTasks.push(queryTable[i].id);
                }
        }
        formData.append("tasks", detectionTasks);

        try
        {
                const response = await fetch("https://cis655-vision-api-project.ue.r.appspot.com/get-image-description", 
                {
                        method: "POST",
                        body: formData,
                })
                const result = await response.json();
                console.log("Server Response:", result);
                document.getElementById("Output").innerText = result;
        } catch(error)
        {
                console.error("Error fetching description:", error);
        }
}

function getCheckedBoxes()
{
        console.log('The checkboxes have the following values:\n');
        var checkboxes = document.getElementsByClassName("checkbox")
        for(var i = 0; i < checkboxes.length; i++)
        {
                queryTable[i].checked = checkboxes[i].checked;
                console.log(queryTable[i].id + ':' + queryTable[i].checked)
        }

}