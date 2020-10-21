import { Component, OnInit } from '@angular/core';
// Importar modelo de Sensor
import { Sensor } from "./sensor.model"
//Importar servicio
import { SensorService } from './sensor.service';

@Component({
  selector: 'app-sensor',
  templateUrl: './sensor.component.html',
  styleUrls: ['./sensor.component.scss']
})
export class SensorComponent implements OnInit {
  // Variable que contendra la lista de sensores
  sensors: Sensor[]
  //Vairable que contendra el profesor seleccionado
  selectedSensor: Sensor;

  // Importar el servicio en el constructor
  constructor(private sensorService: SensorService) { }

  ngOnInit(): void {
    //Llamar a la funcion al inicializar el componente
    this.getSensors();
  }

  //Metodo que obtiene los sensores del servicio
  getSensors(): void {
    //Suscribir la variable sensors al resultado obtenido por el servicio
    //de manera asincronica
    this.sensorService.getSensors()
      .subscribe(sensors => this.sensors = sensors["sensors"]);
  }

  //Metodo que carga el sensor seleccionado a la variable selectedSensor
  onSelect(sensor: Sensor): void {
    this.selectedSensor = sensor;
  }

  //Funcion para eliminar sensores
  delete(sensor: Sensor): void {
    this.sensorService.deleteSensor(sensor.id)
      .subscribe(data => {
        this.getSensors();
      })
  }

}
