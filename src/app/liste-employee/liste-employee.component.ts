import { Component, Input, OnInit } from '@angular/core';
import { EmployeeService } from '../services/employee';
import {FormsModule} from '@angular/forms';
import { Employee } from '../employee';
import {Router} from '@angular/router';

@Component({
  selector: 'app-liste-employee',
  templateUrl: './liste-employee.component.html',
  styleUrls: ['./liste-employee.component.scss', '../home/home.component.scss']
})
export class ListeEmployeeComponent implements OnInit {

  constructor(private employeeService: EmployeeService, private routes:Router) { }
  emp_headers= ["Matricules", "Nom", "Prenom", "Email", "Actions"];
  allEmployee: Employee[] = [];

  ngOnInit(): void {
    this.employeeService.getAllEmp().subscribe((response: any)=>{
      this.allEmployee= response[0];
      console.log(this.allEmployee);
      console.log(this.allEmployee[1].email);
    });
  }

  addEmployee():void{
    this.routes.navigate(['addEmployee']);
  }

  remove():void{
    
  }

  

}
