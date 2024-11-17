import express from 'express';
import logger from 'morgan';
import { Server } from 'socket.io';
import { createServer } from 'node:http';
import axios from 'axios';

const port = process.env.PORT ?? 5000;

const app = express();
const server = createServer(app);

const io = new Server(server, {
    connectionStateRecovery: {}
});

io.on('connection', (socket) => {
    console.log('A user connected');    
    
    socket.on('disconnect', () => {
        console.log('A user disconnected');
    });

    socket.on('chat message', async (message) => {        
        try {
            const response = await axios.post('http://127.0.0.1:5000/predict', {
                pregunta: message             
            });
            
            // Enviar la respuesta procesada al cliente
            io.emit('chat message', {
                pregunta: message,
                respuesta: response.data.respuesta
            });
        } catch (error) {
            console.error('Error al consumir la API Flask:', error);
            io.emit('chat message', { 
                pregunta: message, 
                respuesta: 'Ocurrió un error al procesar tu mensaje.' 
            });
        }
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
