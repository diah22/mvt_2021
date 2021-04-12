import { Component, OnInit } from '@angular/core';
import { SessionService } from '../services/session';

@Component({
  selector: 'app-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.scss', '../home/home.component.scss']
})
export class SessionComponent implements OnInit {

  constructor(private sessionService: SessionService) { }

  ngOnInit(): void {
  }

  launchWebcam(){
    this.sessionService.launchWebcam().subscribe(response=>console.log(response));
  }

}
