import { Subject } from 'rxjs';
import { Injectable } from '@angular/core';
import { WebsocketService } from './websocket.service';
import { map } from "rxjs/operators";

export class MessagePayload {
	msg: string;
	name: string = "user"
}

@Injectable()
export class ChatService {
	public readonly responses: Subject<string> = new Subject<string>();
	messages: Subject<any>;

	constructor(private wsService: WebsocketService) {
		this.messages = <Subject<any>>wsService
			.connect()
			.pipe(map((response: any): any => {
				return response;
			}))

		this.messages.subscribe(msg => {
			if(msg['sender'] != "user")
				this.responses.next(msg['msg'])
		})
	}

	public submit(text: string): void {
		var message: MessagePayload = new MessagePayload();
		message.msg = text;
		this.messages.next(message);
	}
}
