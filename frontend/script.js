function start()
{
        fetch("https://cis655-vision-api-project.ue.r.appspot.com/get-image-description")
        .then(response => response.json())
        .then(data =>
        {
                console.log(data)
                document.getElementById("Problem").innerText = data;
        })
        .catch(error => console.error("Error fetching description:", error));
}