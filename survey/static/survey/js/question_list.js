function answerQuestion(obj){
    $.ajax({
        data: {
            question_pk: $(obj).attr("data-question"),
            value: $(obj).attr("data-value"),
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        type: 'POST',
        url: 'question/answer',
        success: function(response) {
            console.log("Response", response['ok']);
            if (response['ok']) location.reload();
            else alert("Error al completar su solicitud.");
            
        }
    });
};

function likeQuestion(obj){
    $.ajax({
        data: {
            question_pk: $(obj).attr("data-question"),
            liked: 'liked',
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        type: 'POST',
        url: 'question/like',
        success: function(response) {
            console.log("Response", response['ok']);
            if (response['ok']) location.reload();
            else alert("Error al completar su solicitud.");
            
        }
    });
};

function dislikeQuestion(obj){
    $.ajax({
        data: {
            question_pk: $(obj).attr("data-question"),
            liked: 'disliked',
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        type: 'POST',
        url: 'question/like',
        success: function(response) {
            console.log("Response", response['ok']);
            if (response['ok']) location.reload();
            else alert("Error al completar su solicitud.");
            
        }
    });
};