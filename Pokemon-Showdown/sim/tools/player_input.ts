/**
 * Takes input from the user to run a battle.
 */

import {ObjectReadWriteStream} from '../../lib/streams';
import {BattlePlayer} from '../battle-stream';
import {PRNG, PRNGSeed} from '../prng';

export class Player_input extends BattlePlayer {
	protected readonly move: number;
	protected readonly mega: number;
	protected readonly prng: PRNG;

	constructor(
		playerStream: ObjectReadWriteStream<string>,
		options: {move?: number, mega?: number, seed?: PRNG | PRNGSeed | null } = {},
		debug: boolean = false,
		name: string = "NoneGiven"
	) {
		super(playerStream, debug);
		this.move = options.move || 1.0;
		this.mega = options.mega || 0;
		this.prng = options.seed && !Array.isArray(options.seed) ? options.seed : new PRNG(options.seed);
		//The player name is used for debugging and writing weights to file.
		this.name = name;
		this.reader = require("readline");
	}

        //https://stackoverflow.com/questions/18193953/waiting-for-user-to-enter-input-in-node-js
        askQuestion(query) {
                const rl = this.reader.createInterface({
                        input: process.stdin,
                        output: process.stdout,
                });
                return new Promise(resolve => rl.question(query, ans => {
                        rl.close();
                        resolve(ans);
                }));
        }

	receiveError(error: Error) {
		console.log(error);
		console.log(crash);
	}

	newStream(playerStream: ObjectReadWriteStream<string>) {
		this.stream = playerStream;
	}

	async receiveRequest(request: AnyObject) {
		if (request.wait) {
			// wait request. do nothing.
		} else if (request.forceSwitch || request.active) {
                        // Check switches and moves for legality. Adapted from random-player-ai
                        let [canMegaEvo, canUltraBurst, canZMove] = [true, true, true];
                        const pokemon = request.side.pokemon;
                        const chosen: number[] = [];
                        const choices = request.active.map((active: AnyObject, i: number) => {
                                if (pokemon[i].condition.endsWith(` fnt`)) return `pass`;
                                canMegaEvo = canMegaEvo && active.canMegaEvo;
                                canUltraBurst = canUltraBurst && active.canUltraBurst;
                                canZMove = canZMove && !!active.canZMove;
                                let canMove = [1, 2, 3, 4].slice(0, active.moves.length).filter(j => (
                                        // not disabled
                                        !active.moves[j - 1].disabled
                                        // NOTE: we don't actually check for whether we have PP or not because the
                                        // simulator will mark the move as disabled if there is zero PP and there are
                                        // situations where we actually need to use a move with 0 PP (Gen 1 Wrap).
                                )).map(j => ({
                                        slot: j,
                                        move: active.moves[j - 1].move,
                                        target: active.moves[j  - 1].target,
                                        zMove: false,
                                }));
                                if (canZMove) {
                                        canMove.push(...[1, 2, 3, 4].slice(0, active.canZMove.length)
                                                .filter(j => active.canZMove[j - 1])
                                                .map(j => ({
                                                        slot: j,
                                                        move: active.canZMove[j - 1].move,
                                                        target: active.canZMove[j - 1].target,
                                                        zMove: true,
                                                })));
                                }
                                // Filter out adjacentAlly moves if we have no allies left, unless they're our
                                // only possible move options.
                                const hasAlly = !pokemon[i ^ 1].condition.endsWith(` fnt`);
                                const filtered = canMove.filter(m => m.target !== `adjacentAlly` || hasAlly);
                                canMove = filtered.length ? filtered : canMove;
                                const moves = canMove.map(m => {
                                        let move = `move ${m.slot}`;
                                        // NOTE: We don't generate all possible targeting combinations.
                                        if (request.active.length > 1) {
                                                if ([`normal`, `any`, `adjacentFoe`].includes(m.target)) {
                                                        move += ` ${1 + Math.floor(this.prng.next() * 2)}`;
                                                }
                                                if (m.target === `adjacentAlly`) {
                                                        move += ` -${(i ^ 1) + 1}`;
                                                }
                                                if (m.target === `adjacentAllyOrSelf`) {
                                                        if (hasAlly) {
                                                                move += ` -${1 + Math.floor(this.prng.next() * 2)}`;
                                                        } else {
                                                                move += ` -${i + 1}`;
                                                        }
                                                }
                                        }
                                        if (m.zMove) move += ` zmove`;
                                        return {choice: move, move: m};
                                });

                                const canSwitch = [1, 2, 3, 4, 5, 6].filter(j => (
                                        pokemon[j - 1] &&
                                        // not active
                                        !pokemon[j - 1].active &&
                                        // not chosen for a simultaneous switch
                                        !chosen.includes(j) &&
                                        // not fainted
                                        !pokemon[j - 1].condition.endsWith(` fnt`)
                                ));
                                const switches = active.trapped ? [] : canSwitch;
                                return [moves, switches];
                        });
                        console.log('actionspace' + JSON.stringify(choices)); 
                        await new Promise(resolve => setTimeout(resolve, 2));;
                        // In the future, it should be possible to copy-paste the code from I think it was random_player_AI to see which actions are valid.
                        // This will be more consistent than the current solution.

                        console.log(JSON.stringify(request));
                        // This lets pkmn_env.py to stop reading input. This is something I should have done a long time ago.
                        console.log("DEADBEEF");
                        let ans = await this.askQuestion("");
                        this.choose(ans);
                } else if (request.Victory == "yes" || request.Victory == "no") {
                        console.log(this.name + request.Victory);
                } else {
			// team preview?
			this.choose(this.chooseTeamPreview(request.side.pokemon));
		}
	}

	protected chooseTeamPreview(team: AnyObject[]): string {
		return `default`;
	}
}
