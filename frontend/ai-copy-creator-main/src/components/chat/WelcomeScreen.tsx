import { Sparkles, Zap, Target, PenTool } from "lucide-react";

const suggestions = [
	{
		icon: PenTool,
		title: "Copy para anúncio",
		description: "Crie textos persuasivos para Facebook e Instagram Ads",
		type: "anuncios",
	},
	{
		icon: Target,
		title: "Headlines magnéticas",
		description: "Gere títulos que capturam atenção instantaneamente",
		type: "landing-pages",
	},
	{
		icon: Zap,
		title: "Email marketing",
		description: "Escreva emails que convertem e engajam sua audiência",
		type: "emails",
	},
];

interface WelcomeScreenProps {
	onSuggestionClick: (suggestion: string, copyType?: string) => void;
}

const WelcomeScreen = ({ onSuggestionClick }: WelcomeScreenProps) => {
	return (
		<div className="flex-1 flex flex-col items-center justify-center p-8 animate-fade-in">
			<div className="w-16 h-16 rounded-2xl bg-primary flex items-center justify-center mb-6 animate-pulse-glow">
				<Sparkles className="w-8 h-8 text-primary-foreground" />
			</div>

			<h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2 text-center">
				Como posso ajudar você hoje?
			</h1>
			<p className="text-muted-foreground text-center mb-8 max-w-md">
				Sou seu assistente de copywriting. Crio textos persuasivos, headlines
				magnéticas e conteúdo que converte.
			</p>

			<div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-3xl">
				{suggestions.map((suggestion, index) => (
					<button
						key={index}
						onClick={() => onSuggestionClick("", suggestion.type)}
						className="group p-4 rounded-xl bg-secondary border border-border hover:border-primary hover:bg-muted transition-all duration-200 text-left animate-slide-in"
						style={{ animationDelay: `${index * 100}ms` }}
					>
						<suggestion.icon className="w-6 h-6 text-primary mb-3 group-hover:scale-110 transition-transform" />
						<h3 className="font-medium text-foreground mb-1">
							{suggestion.title}
						</h3>
						<p className="text-sm text-muted-foreground">
							{suggestion.description}
						</p>
					</button>
				))}
			</div>
		</div>
	);
};

export default WelcomeScreen;
