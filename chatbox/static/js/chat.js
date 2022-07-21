// send message

const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const sendto = JSON.parse(document.getElementById('json-sendto').textContent);

const socket = new WebSocket(
    'ws://'
    +window.location.host
    +'/ws/chat/'
    +id
    +'/'
);

socket.onopen = function(event) {
    console.log('Connection established');
    console.log(event);
}

socket.onclose = function(event) {
    console.log('Connection closed');
}

socket.onerror = function(event) {
    console.log(event);
}

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    // the message is from others
    if(data.username == message_username) {
        document.querySelector('#chat-body').innerHTML += `
                                <td>
                                    <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">
                                        ${data.message}
                                    </p>
                                </td>`
    }
    else {
        document.querySelector('#chat-body').innerHTML += `
                                <td>
                                    <p class="bg-primary p-2 mt-2 ml-5 shadow-sm text-white float-left rounded">
                                        ${data.message}
                                    </p>
                                </td>`
    }
}

document.querySelector('#chat-message-submit').onclick = function() {
    const message_input = document.querySelector('#message_input');
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message': message,
        'username':message_username,
        'id': sendto
    }));

    message_input.value = '';
    console.log(id, message_username);
}
