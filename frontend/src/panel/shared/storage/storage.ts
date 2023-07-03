
export class Storage {
    static set(key: string, value: string) {
        window.localStorage.setItem(key, value);
    }

    static get(key: string) {
        return window.localStorage.getItem(key);
    }

    static remove(key: string) {
        window.localStorage.removeItem(key);
    }
}