import {UserDto} from "../dto/user_dto";
import {HeatgerBackend} from "../../heatger_backend";
import {HomeAssistant} from "custom-card-helpers";


export async function LoginQuery(hass: HomeAssistant, user: UserDto): Promise<boolean> {
    const api = await HeatgerBackend.build(hass)
    const response = await api.post<string>('login', user).then(r => r);
    if(response.status === 401) {
        console.log('wrong username/password')
        return false;
    }
    await HeatgerBackend.setToken(response.data)
    return true;
}