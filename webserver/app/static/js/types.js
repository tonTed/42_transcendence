/**
 * @typedef {"not_started" | "in_progress" | "finished"} Status
 */

/**
 * @typedef {Object} Player
 * @property {number} id - player id
 * @property {string} name - player name
 */

/**
 * @typedef {Object} Game
 * @property {number} id - game id
 * @property {Player} player1 - player 1 object
 * @property {Player} player2 - player 2 object
 * @property {Status} status - game status
 * @property {number} winner - game winner
 * @property {number} player1_score - player 1 score
 * @property {number} player2_score - player 2 score
 */

/**
 * @typedef {Object} Tournament
 * @property {number} id - tournament id
 * @property {Status} status - tournament status
 * @property {Game[]} games - array of games
 */

export /**
 * @type {Player}
 */
/**
 * @type {Game}
 */
/**
 * @type {Tournament}
 */ {};
