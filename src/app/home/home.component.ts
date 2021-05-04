import { Component, OnInit } from '@angular/core';
import {PresenceService} from '../services/presence';
import {Employee} from '../employee';
import {Presence} from '../presence';
import {Router} from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss', '../login/login.component.scss', '../liste-employee/liste-employee.component.scss']
})
export class HomeComponent implements OnInit {
  presence: Presence[]= [];
  constructor(private presenceService: PresenceService) { }

  ngOnInit(): void {
    this.presenceService.findAllPresence().subscribe((response: any)=>{
      console.log(response[0]);
      this.presence= response[0];
    })
  }

}
