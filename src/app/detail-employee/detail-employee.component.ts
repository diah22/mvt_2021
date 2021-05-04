import { Component, OnInit, Input } from '@angular/core';
import {Router} from '@angular/router';
import {ActivatedRoute} from '@angular/router';
import { Employee } from '../employee';
import {EmployeeService} from '../services/employee';

@Component({
  selector: 'app-detail-employee',
  templateUrl: './detail-employee.component.html',
  styleUrls: ['./detail-employee.component.scss', '../home/home.component.scss', '../liste-employee/liste-employee.component.scss']
})
export class DetailEmployeeComponent implements OnInit {
  matr: string |null| undefined;
  //empl: Employee[]= [];
  //empl: Employee[]= [];
  // @Input() empl: Employee={matricules:'', nom:'', prenom:'', email:'', image:''};
  //empl: Employee[]= [];
  //empl: Employee[]= [];
  // @Input() empl: Employee={matricules:'', nom:'', prenom:'', email:'', image:''};
  @Input()
  empl!: Employee[];
  result:any;
  constructor(private route: ActivatedRoute,
               private employeeService: EmployeeService,
               private router: Router) {
                }

  ngOnInit(): void {
    this.getUser();
  }

  getUser():void{
    this.matr= this.route.snapshot.paramMap.get('matricules');
    this.employeeService.getOneEmp(this.matr).subscribe((employee) => {
      this.empl= employee[0];
      console.log(this.empl);
      console.log(this.empl[0].matricules);
    });
  }

  updateEmployee(): void{
    this.employeeService.updateEmp(this.empl).subscribe(response =>{
      this.result= response;
      if(this.result.response == 'success'){
        this.router.navigate(['listEmployee']);
      }
    })
  }

}
