firstNumber = 0;
secondNumber = 0;
operator = "+";
answer = 0;
score = 0;

function start()
{
        getMathProblem();
        document.getElementById("Start").innerText="Submit";
        document.getElementById("Start").onclick=checkAnswer;
}

function getMathProblem()
{
        fetch("https://cis655-vision-api-project.ue.r.appspot.com/get-problem")
        .then(response => response.json())
        .then(data =>
        {
                firstNumber = data.firstNumber;
                secondNumber = data.secondNumber;
                operator = data.operator;
                document.getElementById("Problem").innerText = firstNumber + " " + operator + " " + secondNumber + " = ?";
        })
        .catch(error => console.error("Error fetching math problem:", error));
}

function solveProblem()
{
        switch(operator)
        {
                case "-":
                        answer = (parseInt(firstNumber) - parseInt(secondNumber)).toString();
                        break;
                case "*":
                        answer = (parseInt(firstNumber) * parseInt(secondNumber)).toString();
                        break;
                case "/":
                        answer = (Math.floor(parseInt(firstNumber) / parseInt(secondNumber))).toString();
                        break;
                default:
                        answer = (parseInt(firstNumber) + parseInt(secondNumber)).toString();

        }
}

function checkAnswer()
{
        userAnswer = document.getElementById("answer").value;
        solveProblem();
        console.log("answer: " + answer);
        if(userAnswer == answer)
        {
                score += 1;
                document.getElementById("Score").innerText = "Score: " + score;
        }
        getMathProblem();
}