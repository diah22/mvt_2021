import { Component,OnInit, Input } from '@angular/core';
import { AdminService } from '../services/admin';
import {Location} from '@angular/common';
import {Admin} from '../admin';
import {Router} from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit{
  @Input() admin:Admin={email:'', password: '', id:'', nom:'', prenom:''};
  result: any;
  isAuth:false | undefined;

  ngOnInit(): void {
    
  }

  constructor(private adminService: AdminService, 
                  private location: Location, 
                      private routes: Router){}

  signin(): void{
    this.adminService.signin(this.admin).subscribe(response=> {
      this.result= response;
      if(this.result.msg == 'success'){
        this.routes.navigate(['home']);
      }
    })
  }


  title = 'angular-flask';

}
