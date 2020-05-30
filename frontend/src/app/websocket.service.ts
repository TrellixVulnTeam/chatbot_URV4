import { Injectable } from '@angular/core';
import * as io from 'socket.io-client';
import { Observable, Subject } from 'rxjs';
import { environment } from '../environments/environment';


@Injectable()
export class WebsocketService {

  private socket: SocketIOClient.Socket;

  constructor() { }

  connect(): Subject<MessageEvent> {
    this.socket = io(environment.ws_url);
    console.log(this.socket);

    let observable = new Observable(observer => {
      this.socket.on('message', (data) => {
        console.log("Received message from Websocket Server")
        observer.next(data);
      })
      return () => {
        this.socket.disconnect();
      }
    });

    let observer = {
      next: (data: Object) => {
        this.socket.emit('text', JSON.stringify(data));
      },
    };

    return Subject.create(observer, observable);
  }

}