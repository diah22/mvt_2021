import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {FormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {RouterModule, Routes} from '@angular/router';
import {MDBBootstrapModule} from 'angular-bootstrap-md';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { ListeEmployeeComponent } from './liste-employee/liste-employee.component';
import { AbsenceComponent } from './absence/absence.component';
import { SessionComponent } from './session/session.component';
import { AddEmployeeComponent } from './add-employee/add-employee.component';
import { DetailEmployeeComponent } from './detail-employee/detail-employee.component';


const routes: Routes= [
  {path:'home', component: HomeComponent},
  {path:'', redirectTo:'/login', pathMatch:'full'},
  {path:'login', component: LoginComponent},
  {path:'listEmployee', component: ListeEmployeeComponent},
  {path:'detailEmployee/:matricules', component: DetailEmployeeComponent},
  {path:'absence', component: AbsenceComponent},
  {path: 'session', component: SessionComponent},
  {path:'addEmployee', component:AddEmployeeComponent}
];


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    ListeEmployeeComponent,
    AbsenceComponent,
    SessionComponent,
    AddEmployeeComponent,
    DetailEmployeeComponent,
 
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    MDBBootstrapModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
