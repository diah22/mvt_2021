
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Employee } from '../employee';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({ providedIn: 'root' })
export class EmployeeService {

  private userUrl = 'http://localhost:5000';  // URL to REST API

  constructor(private http: HttpClient) { }

  
  signin(employee: Employee) {
	//console.log(user);
    return this.http.post(this.userUrl + '/signin', employee, httpOptions);
  }

  saveImage(employee: Employee){
      return this.http.post(this.userUrl+'/webcam',employee, httpOptions);
  }

  getAllEmp(){
    return this.http.get(this.userUrl+'/getAllEmployee', httpOptions);
  }

  getOneEmp(matr: string |null):Observable<any>{
    return this.http.get<Employee>(this.userUrl+`/getOneEmployee/${matr}`);
  }

  updateEmp(employee: Employee[]) {
    return this.http.post(this.userUrl+'/update', employee, httpOptions);
  }
  
  
}