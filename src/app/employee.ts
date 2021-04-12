export class Employee{
    matricules: string;
    nom: string;
    prenom: string;
    email: string;
    image: any;

    constructor(matricules: string, nom: string, prenom:string, email:string, image:any){
        this.matricules= matricules;
        this.nom= nom;
        this.prenom= prenom;
        this.email= email;
        this.image= image;
    }
}