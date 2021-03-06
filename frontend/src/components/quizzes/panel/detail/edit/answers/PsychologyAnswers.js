import React from 'react'

import { MdQuestionAnswer } from 'react-icons/md'

import { DragDropContext, Draggable, Droppable } from 'react-beautiful-dnd'
import Answer from './Answer'

class PsychologyAnswers extends Answer {
	constructor(props) {
		super(props)

		this.onDragEnd = this.onDragEnd.bind(this)
	}

	onDragEnd = (result) => {
		if (!result.destination) return

		const { source, destination } = result

		if (source.droppableId !== destination.droppableId) {
			const sourceColumn = this.props.questions[
				this.props.questionIndex
			].answers.filter(
				(answer) =>
					answer.id.toString() === source.droppableId.toString()
			)[0]
			const destColumn = this.props.questions[
				this.props.questionIndex
			].answers.filter(
				(answer) =>
					answer.id.toString() === destination.droppableId.toString()
			)[0]

			const sourceItems = [...sourceColumn.results]
			const destItems = [...destColumn.results]
			const [removed] = sourceItems.splice(source.index, 1)
			destItems.splice(destination.index, 0, removed)

			this.props.setQuestions(
				this.props.questions.map((question, index) => {
					// if this is the question where our answers are
					if (index === this.props.questionIndex)
						return {
							...question,
							answers: question.answers.map((answer) => {
								if (
									answer.id.toString() ===
									source.droppableId.toString()
								)
									return {
										...answer,
										results: sourceItems,
									}
								else if (
									answer.id.toString() ===
									destination.droppableId.toString()
								)
									return {
										...answer,
										results: destItems,
									}

								return answer
							}),
						}

					return question
				})
			)
		}
	}

	render() {
		const { hasChanged } = this.state
		const { punctationLength } = this.props

		const answers = this.props.answers.map((answer, index) => (
			<div className="form-control" key={index}>
				<label className="form-control__label">
					Answer {index + 1}:
				</label>
				<div className="icon-form">
					<span className="icon">
						<MdQuestionAnswer />
					</span>

					<input
						type="text"
						data-id={index}
						onChange={this.onChangeTextField}
						name="answer"
						value={this.props.answers[index].answer}
						className="form-control__input"
						placeholder={`Pass the ${index + 1} answer...`}
						maxLength="100"
						required
					/>
				</div>
				<Droppable droppableId={answer.id.toString()}>
					{(provided, snapshot) => (
						<div
							{...provided.droppableProps}
							ref={provided.innerRef}
							className={`droppable ${
								snapshot.isDraggingOver ? 'draggingOver' : ''
							}`}
						>
							{answer.results?.map((result, index) => (
								<Draggable
									key={result.id.toString()}
									draggableId={result.id.toString()}
									index={index}
								>
									{(provided, snapshot) => (
										<div
											ref={provided.innerRef}
											{...provided.draggableProps}
											{...provided.dragHandleProps}
											className={`draggable ${
												snapshot.isDragging
													? 'dragging'
													: ''
											}`}
										>
											{result.result}
										</div>
									)}
								</Draggable>
							))}
							{provided.placeholder}
						</div>
					)}
				</Droppable>
			</div>
		))

		return (
			<div className="card">
				<div className="card__body">
					<DragDropContext
						onDragEnd={(result) => this.onDragEnd(result)}
					>
						{answers}
					</DragDropContext>

					<hr />
					<div className="card__body">
						<div className="inline-btns">
							<button
								type="button"
								className={`btn ${
									answers.length >= punctationLength
										? 'btn__disabled'
										: ''
								}`}
								onClick={this.addAnswer}
							>
								Add Answer
							</button>
							<button
								type="button"
								className={`btn btn__danger ${
									answers.length <= 2 ? 'btn__disabled' : ''
								}`}
								onClick={this.removeAnswer}
							>
								Remove Answer
							</button>
						</div>
						<br /> <br />
						<button
							type="reset"
							onClick={this.resetForm}
							className={`btn ${
								!hasChanged ? 'btn__disabled' : ''
							}`}
						>
							Cancel
						</button>
					</div>
				</div>
			</div>
		)
	}
}

export default PsychologyAnswers
