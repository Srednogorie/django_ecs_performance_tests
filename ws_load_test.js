import ws from 'k6/ws';
import { check } from 'k6';

export const options = {
  vus: 50,
  duration: '60s',
};

export default function () {
  const url = 'ws://127.0.0.1:8001/ws/chat/testroom/';

  const res = ws.connect(url, function (socket) {
    socket.on('open', () => {
      socket.send(JSON.stringify({ type: 'chat.message', t: Date.now(), message: 'On socket open' }));
    });

    socket.on('message', (msg) => {
      const data = JSON.parse(msg);
      const latency = Date.now() - data.t;
      console.log('latency ms:', latency, "data", data);
    });

    socket.setInterval(() => {
      socket.send(JSON.stringify({ type: 'chat.message', t: Date.now(), message: 'On interval' }));
    }, 10000);

    socket.setTimeout(() => {
      socket.close();
    }, 60000);
  });

  check(res, { 'connected': (r) => r && r.status === 101 });
}
