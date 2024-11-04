import express from 'express';
import logger from 'morgan';
import { Server } from 'socket.io';
import { createServer } from 'node:http';

const port = process.env.PORT ?? 3000;


const app = express();
const server = createServer(app);
//Se crea el servidor y se crea un tipo de espera de conexione para volver a conectar a los clientes
const io = new Server(server, {
    connectionStateRecovery: {}
});


io.on('connection', (socket) => {
    console.log('A user connected');    
    socket.on('disconnect', () => {
        console.log('A user disconnected');
    });

    socket.on('chat message', (message) => {
        io.emit('chat message', message);
    });
});

app.use(logger('dev'));
app.use(express.static('assets'));

app.get('/', (req, res) => {
    res.sendFile(process.cwd() + '/client/index.html');
});

server.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});