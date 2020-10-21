import { Injectable } from '@angular/core';
// Importar modelo de Sensor
import { Sensor } from "./sensor.model"
//Importar observable
import { Observable, of } from 'rxjs';
//Importar librerías
import { HttpClientModule, HttpClient, HttpErrorResponse } from '@angular/common/http';
//Importar URL de la API
import { API_URL } from '../env';

@Injectable({
  providedIn: 'root'
})
export class SensorService {

  //Agregar el cliente al constructor
  constructor(private http: HttpClient) { }

  //Funcion que obtiene los sensores
  getSensors(): Observable<Sensor[]> {
    //Hacer request a la API
    return this.http.get<Sensor[]>(API_URL + '/sensors');
  }

  deleteSensor(id) {
    return this.http.delete<Sensor>(API_URL + '/sensor/' + id);
  }

  //Funcion para el manejo de errores HTTP
  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }
}
