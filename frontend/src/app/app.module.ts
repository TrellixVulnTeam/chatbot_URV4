import { NgModule } from '@angular/core';
import { Component } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ChatModule } from '@progress/kendo-angular-conversational-ui';

import { AppComponent } from './app.component';
import { WebsocketService } from './websocket.service';

@NgModule({
  imports:      [ BrowserModule, BrowserAnimationsModule, ChatModule ],
  declarations: [ AppComponent ],
  providers: [WebsocketService],
  bootstrap:    [ AppComponent ]
})

export class AppModule { }
