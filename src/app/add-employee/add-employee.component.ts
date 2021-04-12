import { Component, OnInit, Input } from '@angular/core';
import {Router} from '@angular/router';
import {EmployeeService} from '../services/employee';
import {Employee} from '../employee';

@Component({
  selector: 'app-add-employee',
  templateUrl: './add-employee.component.html',
  styleUrls: ['./add-employee.component.scss', '../liste-employee/liste-employee.component.scss', '../home/home.component.scss']
})
export class AddEmployeeComponent implements OnInit {

  constructor(private routes: Router, private employeeService: EmployeeService) { }
  @Input() employee: Employee={matricules:'', nom:'', prenom:'', email:'', image:''};

  ngOnInit(): void {
  }
  
  addEmployee():void{
    this.routes.navigate(['addEmployee']);
  }

  saveImage():void{
    this.employeeService.saveImage(this.employee).subscribe(response => {
      console.log(response);
      this.routes.navigate(['listEmployee']);
    });
  }
}
