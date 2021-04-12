import { Binary } from "selenium-webdriver/firefox";

export class Image{
    id: string;
    //photo: Binary;
    matricules: string;

    constructor(id:string, matricules:string){
        this.id= id;
        this.matricules= matricules;
    }
}