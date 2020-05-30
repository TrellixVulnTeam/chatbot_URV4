import { Observable, Subject } from 'rxjs';
import { Injectable } from '@angular/core';
import { WebsocketService } from './websocket.service';
import { map } from "rxjs/operators";

export class MessagePayload {
	msg: string;
	room: string = "ai_team_7"
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
	}

	public submit(question: string): void {
		const length = question.length;
		const answer = `"${question}" contains exactly ${length} symbols.`;

		this.sendMsg(question)
		setTimeout(
			() => this.responses.next(answer),
			1000
		);
	}

	public sendMsg(msg) {
		var message: MessagePayload = new MessagePayload();
		message.msg = msg
		this.messages.next(message);
	}
}
