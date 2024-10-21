import express from 'express';
import logger from 'morgan';
import { Server } from 'socket.io';
import { createServer } from 'node:http';
import sqlite from 'sqlite3';

const db = new sqlite.Database(':memory:');
const port = process.env.PORT ?? 3000;

// Execute SQL statements from strings.
await db.exec(`
   CREATE TABLE IF NOT EXISTS consultas(      
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Tipo_Documento varchar(2),
        numero_documento varchar(10),
        consulta varchar(100)
  )
`);

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

app.get('/', (req, res) => {
    res.sendFile(process.cwd() + '/client/index.html');
});

server.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});