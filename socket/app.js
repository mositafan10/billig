const { Console } = require('console');

var app = require('express')();
var http = require('http').createServer(app);
const io = require("socket.io")(http, {
    cors: {
        origin: "http://localhost:3000",
        }
  });

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
  console.log('a user connected :' + socket.id);
  console.log(socket.rooms)

  socket.on('createJoinRoom', function(data) {
    socket.join(data.chatID);
    console.log(socket.rooms)
  });

  socket.on('createJoinOfferRoom', function(data) {
    socket.join(data.offerID);
    console.log(socket.rooms)
  });

  socket.on('offerChanged',(offerRoom)=>{
    console.log('offer change')
    console.log(offerRoom)
    io.to(offerRoom).emit("updateOffer");
  })

  socket.on("private message", (data) => {
    socket.to(data.chatID).emit("shouldUpdateMessage", data.msg);
  })

  socket.on('leaveRoom', function(room) {
    io.to(room).emit('onlineStatus',false)
    console.log('user leaves room now')
  });

  socket.on('disconnect', () => {
    console.log('a user disconnected' + socket.id);
  })

});

http.listen(3001, () => {
  console.log('listening on *3001');
});