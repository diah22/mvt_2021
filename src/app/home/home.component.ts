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
  is_permitted_all:boolean= false;
  is_show_only: boolean= true;
  buttonName= 'Voir plus';
  presence: Employee[]= [];
  constructor(private presenceService: PresenceService) { }

  ngOnInit(): void {
    this.presenceService.findAllPresence().subscribe((response: any)=>{
      console.log(response[0]);
      this.presence= response[0];
    })
  }

  tooglePresence(): void {
    this.is_permitted_all= !this.is_permitted_all;

    if(this.is_permitted_all)
    {
      this.is_show_only = false;
      this.buttonName= 'Retour';
    }
    else
    {
      this.is_show_only= true;
      this.buttonName = 'Voir plus';
    }
  }
}
