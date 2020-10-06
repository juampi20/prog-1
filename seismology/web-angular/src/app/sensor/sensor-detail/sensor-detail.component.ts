import { Component, Input, OnInit } from '@angular/core';
import { Sensor } from "../sensor.model"

@Component({
    selector: 'app-sensor-detail',
    templateUrl: './sensor-detail.component.html',
    styleUrls: ['./sensor-detail.component.scss']
})
export class SensorDetailComponent implements OnInit {
    @Input() sensor: Sensor;
    constructor() { }

    ngOnInit(): void {
    }

}
