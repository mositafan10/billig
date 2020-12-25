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

const users = {};
// we can set limit for users in private room
io.on('connection', (socket) => {
  console.log('a user connected :' + socket.id);
  socket.on('create_join_room', function(data) {
    console.log('data',data)
    socket.join(data.chatID);
    users[socket.id] = data.userID;
    console.log(users)
    const count = Object.keys(users).length
    console.log(count)
    io.in(data.chatID).emit("online",count);
    socket.on("private message", () => {
      socket.in(data.chatID).emit("shouldUpdate");
    })
    // socket.on("private message", (mas) => {
    //   socket.to(data.chatID).emit("shouldUpdate",mas);
    // })
    
  });

  socket.on('leave_room', function(room) {
    socket.to(room).emit("online",false);
    console.log('user leaves room now')
    delete users[socket.id];
    console.log(users)
    socket.leave(room);
    // socket.on("private message", (mas) => {
    //     socket.to(room).emit("shouldUpdate",mas[0].text);
    // })
  });

  socket.on('disconnect', () => {
    console.log('a user disconnected' + socket.id);
  })

});

http.listen(3001, () => {
  console.log('listening on *3001');
});