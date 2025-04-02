var queryTable = [
        {id: "LABEL_DETECTION", checked: 0, result: "label_annotations", text: "Labels", descriptor: "description"},
        {id: "LANDMARK_DETECTION", checked: 0, result: "landmark_annotations", text: "Landmarks", descriptor: "description"},
        {id: "LOGO_DETECTION", checked: 0, result: "logo_annotations", text: "Logos", descriptor: "description"},
        {id: "DOCUMENT_TEXT_DETECTION", checked: 0, result: "text_annotations", text: "Text", descriptor: "description"},
        {id: "OBJECT_LOCALIZATION", checked: 0, result: "localized_object_annotations", text: "Objects", descriptor: "name"},
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
                displayResults(detectionTasks, result);
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

function displayResults(tasks, result)
{
        const resultDiv = document.getElementById('Results');
        resultDiv.innerHTML = '';

        for(var i = 0; i < queryTable.length; i++)
        {
                const section = queryTable[i].result;
                if(result.data[section])
                {
                        const sectionHeader = document.createElement('h4');
                        sectionHeader.innerText = queryTable[i].text;
                        resultDiv.appendChild(sectionHeader);

                        for (var j = 0; j < result.data[section].length; j++) 
                        {
                                console.log('descriptions: ' + `${queryTable[i].descriptor}: ` + result.data[section][j][queryTable[i].descriptor]);
                                const sectionInfo = document.createElement('p');
                                sectionInfo.innerText = result.data[section][j][queryTable[i].descriptor];
                                resultDiv.appendChild(sectionInfo);
                        }
                }
        }
}