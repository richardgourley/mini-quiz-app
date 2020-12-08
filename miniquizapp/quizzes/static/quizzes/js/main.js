revealAnswersButton = document.getElementById("reveal-answers-button");
quizAnswers = document.getElementById("quiz-answers");

revealAnswersButton.onclick = function(){
	if (quizAnswers.style.display === "block"){
		quizAnswers.style.display = "none";
		revealAnswersButton.innerHTML = "REVEAL ANSWERS!";
	} else {
		quizAnswers.style.display = "block";
		revealAnswersButton.innerHTML = "HIDE ANSWERS!";
	}
}
