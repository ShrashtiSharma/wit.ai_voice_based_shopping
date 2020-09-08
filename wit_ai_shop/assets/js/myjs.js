window.addEventListener("load", initEvent);

function initEvent() {
    mic_play_btn = document.querySelector("#mic-play");
    mic_play_btn.addEventListener("click", hidePause);

    mic_pause_btn = document.querySelector("#mic-pause");
    mic_pause_btn.addEventListener("click", hidePlay);

    var x = document.querySelector("#audio_tag");
    document.querySelector("#audioInput").addEventListener('blur', misunderstand);
    console.log("pa")
}


function misunderstand(obj) {
    var inputVal = parseInt(obj.value);
    if(inputVal > 1) {
        console.log("pp")
        x.play();
    }
}

// misunderstand();


function hidePause() {
    mic_pause_btn.style.display = "block";
    mic_play_btn.style.display = "none";
}
function hidePlay() {
    mic_play_btn.style.display = "block";
    mic_pause_btn.style.display = "none"
}


// function initEvent() {
    // mic_btn = document.querySelector(".microphone");
    // mic_btn.addEventListener("click", toggleMic);
// }


// var flag = false;

// function toggleMic() {
//     if (!flag) {
//         mic_btn.innerHTML = '<i class="fa fa-microphone"></i>';
//         mic_btn.style.background = "#c21c2f";
//     } else {
//         mic_btn.innerHTML = '<i class="fa fa-microphone-slash"></i>';
//         mic_btn.style.background = "#ff5063";
//     }
//     flag = !flag;
// }
