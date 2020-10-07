import { Component, OnInit } from '@angular/core';
import { Sensor } from "./sensor.model"

@Component({
  selector: 'app-sensor',
  templateUrl: './sensor.component.html',
  styleUrls: ['./sensor.component.scss']
})
export class SensorComponent implements OnInit {

  selectedSensor: Sensor;
  sensors: Sensor[] = [
    {
      name: 'Pablo',
      active: true,
      status: true,
      id: 1,
    },
    {
      name: 'Mica',
      active: true,
      status: true,
      id: 2,
    },
    {
      name: "Ivan",
      active: true,
      status: false,
      id: 3,
    },
    {
      name: 'Lu',
      active: true,
      status: true,
      id: 5,
    },
    {
      name: 'Fede',
      active: false,
      status: true,
      id: 4,
    },
  ]

  constructor() { }

  ngOnInit(): void {
  }

}
