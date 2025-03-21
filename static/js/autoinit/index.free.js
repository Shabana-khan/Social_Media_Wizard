import defaultInitSelectors from './initSelectors/free.js';
import { InitMDB } from './init.js';

const initMDBInstance = new InitMDB(defaultInitSelectors);
const initMDB = initMDBInstance.initMDB;

export default initMDB;
