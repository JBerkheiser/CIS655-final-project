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