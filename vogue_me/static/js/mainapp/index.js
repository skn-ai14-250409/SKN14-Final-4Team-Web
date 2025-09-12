const $room      = document.getElementById("chat-area");
const $tmplChat  = document.getElementById("tmpl-chat").content;
const $tmplStyle = document.getElementById("tmpl-style").content;
const TYPE       = {USER:"user", AI:"ai"};
Object.freeze(TYPE);

const curTime = () => {
    let now  = new Date();
    let hour = now.getHours();
    let min  = now.getMinutes();
    let ampm = hour >= 12 ? "PM" : "AM";

    hour = (hour < 10 ? "0" : "") + hour;
    min  = (min  < 10 ? "0" : "") + min;
    return `${hour}:${min} ${ampm}`;
}
const addChat = (data) => {
    let type    = data["type"];
    let msg1    = data["msg1"] || data["msg"];
    let msg2    = data["msg2"];
    let list    = data["list"];
    let voice   = data["voice"];
    let time    = data["time"] || curTime();
    let profileImage = AI_INFO.image;
    let talkerName   = AI_INFO.name;

    type = Object.values(TYPE).includes(type) ? type : TYPE.AI;
    if( type === TYPE.USER ) {
        profileImage = USER_INFO.image;
        talkerName   = USER_INFO.name;
    }

    let $chat = $tmplChat.cloneNode(true).querySelector(".chat");
    $chat.classList.add(type);
    $chat.querySelector(".profile-image").src = profileImage;
    $chat.querySelector(".talker-name").innerText = talkerName;
    $chat.querySelector(".text").innerHTML = msg1.replace(/\r/g,"").replace(/\n/g, "<br/>");
    $chat.querySelector(".chat-time").innerText = time;

    let $ul = $chat.querySelector("ul");
    list = list || [];
    if( ! list.length )
        $chat.querySelector(".style_result").remove();
    else {
        for(let i in list) {
            let data = list[i];
            let $li  = $tmplStyle.cloneNode(true);
            $li.querySelector(".look-link").href = `/detail/${data["id"]}`;
            $li.querySelector(".look-image").src = data["image"];
            $li.querySelector(".look-name").innerText = data["look_name"];
            $li.querySelector(".look-desc").innerText = data["look_desc"];

            $ul.appendChild($li);
        }
    }

    if( msg2 )      $chat.querySelector(".text.optional").innerHTML = msg2;
    else            $chat.querySelector(".text.optional").remove();

    if( voice )     $chat.querySelector(".voice audio").src = voice;
    else            $chat.querySelector(".voice").remove();

    $room.appendChild($chat);
    $chat.scrollIntoView({behavior:"smooth", block:"end"});
}

const firstReaction = resp => {
    if( !resp.ok ) {
        addChat({type:"ai", msg:"뭔가 문제가 있는거 같습니다."});
        console.log(`ERROR : ${resp.status}`);
    }
    else            return resp.json();
}
const secondReaction = json => addChat(json);
const sendQuery = (msg) => {    fetch("http://localhost:8000/chat", {
        method  : "POST",
        headers : { "Content-Type": "application/json" },

        body: JSON.stringify({ message: msg }),   // ← msg → message로 보냄
    })
    .then(firstReaction)
    .then(secondReaction)
    .catch(err => {
        console.error(err);
        addChat({ type: "ai", msg1: "서버 연결에 실패했어요." });
    });
}

const $userInput = document.querySelector(".user_input");
const $sendBtn   = document.querySelector(".chatbox a");
$sendBtn.addEventListener("click", e => {
    const msg = $userInput.value;
    const param = {
        "type"  : TYPE.USER,
        "msg1"  : msg,
    };

    sendQuery(msg);
    addChat(param);
    $userInput.value = "";
});

$userInput.addEventListener("keydown", e => {
    let isEnter = e.key === "Enter";
    e.ctrlKey && isEnter && $sendBtn.click();
});
$userInput.addEventListener("focus", e => e.target.placeholder = "");
$userInput.addEventListener("blur" , e => e.target.placeholder = "메시지를 입력하세요.");
