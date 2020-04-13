/**
 * Tests random AI against human.
 */
import {BattleStream, getPlayerStreams} from '../battle-stream';
import {Dex} from '../dex';
import {MyAI} from '../tools/my_ai';
import {RandomPlayerAI} from '../tools/random-player-ai';
import {Player_input} from '../tools/player_input';
// tslint:disable:no-floating-promises
const spec = {
	formatid: "gen8customgame",
	seed: process.argv[2],
};

if (process.argv[2]) {
	spec.seed = JSON.parse(process.argv[2]);
}
//Give Alice and HughMann two totally arbitary teams which were generated by the random team generator some ways back.


const p1spec = {
	name: "Alice",
	team: 'Swellow||flameorb|guts|bravebird,earthquake,swordsdance,facade||85,85,85,85,85,85||||100|]Ledian||leftovers|swarm|toxic,stealthrock,uturn,roost||85,85,85,85,85,85||||100|]Malamar||leftovers|contrary|sleeptalk,superpower,rest,knockoff||85,85,85,85,85,85||||100|]Houndoom||leftovers|flashfire|darkpulse,nastyplot,hiddenpowergrass,fireblast||85,85,85,85,85,85||,0,,,,||100|]Victreebel||grassiumz|chlorophyll|powerwhip,knockoff,swordsdance,sleeppowder||85,85,85,85,85,85||||100|]Lugia||leftovers|multiscale|psychic,substitute,toxic,whirlwind||85,85,85,85,85,85|N|,,,,,||100|',
};
const p2spec = {
	name: "HughMann",
	team: 'Aggron||leftovers|sturdy|headsmash,heavyslam,aquatail,superpower||85,85,85,85,85,85||||100|]Arceus|arceusfighting|fistplate|multitype|swordsdance,extremespeed,aerialace,dracometeor||85,85,85,85,85,85|N|,,,,,||100|]Dragonite||lumberry|multiscale|dragonclaw,firepunch,roost,earthquake||85,85,85,85,85,85||||100|]Uxie||leftovers|levitate|psyshock,yawn,stealthrock,psychic||85,85,85,85,85,85|N|||100|]Cacturne||leftovers|waterabsorb|swordsdance,seedbomb,suckerpunch,spikes||85,85,85,85,85,85||||100|]Druddigon||lifeorb|sheerforce|dragontail,suckerpunch,gunkshot,aerialace||85,85,85,85,85,85||||100|',
};

//Although I had hoped to remove p1lookup and p2lookup, I need them here because you need Rotom-Heat up above and Rotom down below.
const p1lookup = {
        name: "Alice",
        team: 'Swellow||flameorb|guts|bravebird,earthquake,swordsdance,facade||85,85,85,85,85,85||||100|]Ledian||leftovers|swarm|toxic,stealthrock,uturn,roost||85,85,85,85,85,85||||100|]Malamar||leftovers|contrary|sleeptalk,superpower,rest,knockoff||85,85,85,85,85,85||||100|]Houndoom||houndoominite|flashfire|darkpulse,nastyplot,hiddenpowergrass,fireblast||85,85,85,85,85,85||,0,,,,||100|]Victreebel||grassiumz|chlorophyll|powerwhip,knockoff,swordsdance,sleeppowder||85,85,85,85,85,85||||100|]Lugia||leftovers|multiscale|psychic,substitute,toxic,whirlwind||85,85,85,85,85,85|N|,0,,,,||100|',
};
const p2lookup = {
        name: "HughMann",
	team: 'Aggron||leftovers|sturdy|headsmash,heavyslam,aquatail,superpower||85,85,85,85,85,85||||100|]Arceus|arceusfighting|fistplate|multitype|swordsdance,extremespeed,aerialace,dracometeor||85,85,85,85,85,85|N|,0,,,,||100|]Dragonite||lumberry|multiscale|dragonclaw,firepunch,roost,earthquake||85,85,85,85,85,85||||100|]Uxie||leftovers|levitate|psyshock,yawn,stealthrock,psychic||85,85,85,85,85,85|N|||100|]Cacturne||leftovers|waterabsorb|swordsdance,seedbomb,suckerpunch,spikes||85,85,85,85,85,85||||100|]Druddigon||lifeorb|sheerforce|dragontail,suckerpunch,gunkshot,aerialace||85,85,85,85,85,85||||100|',
};


function spec_to_dict(spec: anyObject, name: string) {
	let pokemonNames = spec.team.split('|');
	pokemonNames = [name + ": " + pokemonNames[0], name + ": " + pokemonNames[11].slice(1), name + ": " + pokemonNames[22].slice(1), name + ": " + pokemonNames[33].slice(1), name + ": " + pokemonNames[44].slice(1), name + ": " + pokemonNames[55].slice(1)];
	let pokemonIndices = [0,0,0,0,0,0]
	let retval = {};
	for (let i in [0,1,2,3,4,5]) {
		for (let j in [0,1,2,3,4,5]) {
			if (pokemonNames[j] < pokemonNames[i]) {
				pokemonIndices[i] += 1;
			}
		}
		retval[pokemonNames[i]] = pokemonIndices[i];
	}
	return retval;
}

const aliceLookup = spec_to_dict(p1lookup, "p1");
const bobLookup = spec_to_dict(p2lookup, "p2");

//Set up the streaming infrastructure.
let streams = getPlayerStreams(new BattleStream(), [aliceLookup, bobLookup]);

//Debug is false.
const p1 = new Player_input(streams.p1, {}, false, "Alice");
const p2 = new Player_input(streams.p2, {}, false, "HughMann");

//Tell the players to start up.
void p1.start();
void p2.start();

/*void (async () => {
        let chunk;
        // tslint:disable-next-line no-conditional-assignment
        while ((chunk = await streams.omniscient.read())) {
                console.log(chunk);
        }
})();*/

void streams.omniscient.write(`>start ${JSON.stringify(spec)}
>player p1 ${JSON.stringify(p1spec)}
>player p2 ${JSON.stringify(p2spec)}`);

