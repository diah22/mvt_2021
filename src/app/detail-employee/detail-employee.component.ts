import { Component, OnInit, Input } from '@angular/core';
import {Routes} from '@angular/router';
import {ActivatedRoute} from '@angular/router';
import { Employee } from '../employee';
import {EmployeeService} from '../services/employee';

@Component({
  selector: 'app-detail-employee',
  templateUrl: './detail-employee.component.html',
  styleUrls: ['./detail-employee.component.scss', '../home/home.component.scss', '../add-employee/add-employee.component.scss']
})
export class DetailEmployeeComponent implements OnInit {
  matr: string |null| undefined;
  //empl: Employee[]= [];
  //empl: Employee[]= [];
  @Input() empl: Employee={matricules:'', nom:'', prenom:'', email:'', image:''};
  constructor(private route: ActivatedRoute,
               private employeeService: EmployeeService) {
                }

  ngOnInit(): void {
    this.getUser();
  }

  getUser():void{
    this.matr= this.route.snapshot.paramMap.get('matricules');
    this.employeeService.getOneEmp(this.matr).subscribe((employee) : any=> {
      this.empl= employee;
      console.log(this.empl);
      console.log(this.empl.matricules);
    });
  }

}
