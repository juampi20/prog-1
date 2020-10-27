import { Component, OnInit } from '@angular/core';
//Importar servicio de Auth
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})

export class LoginComponent implements OnInit {

  email = '';
  password = '';

  constructor(private authService: AuthService) { }

  //Llama a la funcion de login del servicio
  login() {
    this.authService.login(this.email, this.password)
  }

  ngOnInit(): void {
  }

}
