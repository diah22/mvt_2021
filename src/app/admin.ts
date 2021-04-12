export class Admin{
    id: string;
    nom: string;
    prenom: string;
    password: string;
    email:string;

    constructor(id: string, nom:string, prenom:string, password: string, email: string){
        this.id= id;
        this.nom= nom;
        this.prenom= prenom;
        this.password= password;
        this.email= email;
    }


}