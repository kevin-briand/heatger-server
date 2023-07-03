import axios, {Axios, isAxiosError} from "axios";
import {HomeAssistant} from "custom-card-helpers";
import {Storage} from "../shared/storage/storage";


export class HeatgerBackend extends Axios {
    constructor(baseURL: string) {
        if (typeof baseURL === 'undefined') {
            throw new Error('Cannot be called directly');
        }
        super({
            ...axios.defaults,
            baseURL,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                Authorization: Storage.get('api_token')
            },
        })
        this.interceptors.response.use(
            (response) => response,
            async (error) => {
                if (isAxiosError(error) && error.response) {
                    if (error.response.status === 401) {
                        Storage.remove('api_token')
                    }
                }
                return Promise.reject(error);
            }
        );
    }

    static async build(hass: HomeAssistant): Promise<Axios> {
        const deviceInfo = await hass.callWS<any>({type: 'config/device_registry/list', id: 1}).then(r => r.find((r: any) => {
            if (r.name === 'heatger') {
                return r;
            }
        })).catch(() => {
            throw new Error('Ip not found !');
        });
        if(deviceInfo && deviceInfo.connections[0].length !== 0) {
            return new HeatgerBackend(`http://${deviceInfo.connections[0][1]}:5000/`);
        }
        throw new Error('Ip not found !');
    }

    static setToken(token: string) {
        Storage.set('api_token', token)
    }

    static isConnected() {
        return Storage.get('api_token') != null;
    }
}