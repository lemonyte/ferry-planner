/** Get the value of a key in a cache, computing and storing it if the cache has none. */
export const cached = <Key, Value>(cache: Map<Key, Value>, key: Key, compute: () => Value): Value => {
    let value = cache.get(key);
    if (value === undefined) {
        value = compute();
        cache.set(key, value);
    }
    return value;
};
