import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { API_URL } from '../env';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  //Atributo donde se guardara el token
  token;

  constructor(private http: HttpClient, private router: Router) { }

  //Metodo que realiza la request de login
  login(email: string, password: string) {
    this.http.post(API_URL + '/auth/login', { email: email, password: password })
      .subscribe((resp: any) => {
        //Redireccionar a home
        this.router.navigate(['']);
        //Guardar el token
        localStorage.setItem('token', resp.access_token);
      })
  }

  //Metodo de logout
  logout() {
    //Vaciar el token
    localStorage.removeItem('token');
    //Redireccionar a login
    this.router.navigate(['login']);
  }

  //Metodo que indica si el usuario esta o no autenticado
  public get isAuthenticated(): boolean {
    return (localStorage.getItem('token') !== null);
  }

}
