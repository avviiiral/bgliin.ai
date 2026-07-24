import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {

  connect(cameraId: string): Observable<string> {

    const subject = new Subject<string>();

    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';

    const socket = new WebSocket(
      `${protocol}://115.84.171.246:8000/ws/camera/${cameraId}/`
    );

    socket.onmessage = (event) => {
      subject.next('data:image/jpeg;base64,' + event.data);
    };

    socket.onerror = () => {
      subject.complete();
    };

    socket.onclose = () => {
      subject.complete();
    };

    return subject.asObservable();
  }
}